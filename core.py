import os
import requests
from dotenv import load_dotenv
import re
import google.generativeai as genai
from groq import Groq

load_dotenv()


class BookMaker:

    def __init__(self):
        self.api_key_openai = os.environ.get("OPENAI_API_KEY")
        self.api_key_gemini = os.environ.get("GOOGLE_GEMINI")
        self.gemini_model = genai.GenerativeModel("gemini-1.5-flash")
        genai.configure(api_key=self.api_key_gemini)
        self.openai_model = "gpt-4o-mini"
        self.groq_client = Groq(api_key=os.environ.get("GROQ"))

    def call_gemini(self, prompt):
        response = self.gemini_model.generate_content(prompt)
        return response.text

    def call_openai_api(self, prompt):
        headers = {
            "Authorization": f"Bearer {self.api_key_openai}",
            "Content-Type": "application/json",
        }
        data = {
            "model": self.openai_model,
            "messages": [{"role": "user", "content": prompt}],
        }

        response = requests.post(
            "https://api.openai.com/v1/chat/completions", headers=headers, json=data
        )
        if response.status_code == 200:
            result = response.json()
            return result["choices"][0]["message"]["content"]
        else:
            raise Exception(
                f"API call failed with status code {response.status_code}: {response.text}"
            )

    def load_from_file(self, file_path):
        try:
            with open(file_path, "r", encoding="utf-8") as file:
                python_file_contents = file.read()
        except FileNotFoundError:
            print(f"Error: The file {file_path} was not found.")
        except Exception as e:
            print(f"An error occurred: {e}")

        return python_file_contents

    def extract_code_blocks(self, text):
        pattern = r"```(?:\w+)?\n(.*?)```"
        code_blocks = re.findall(pattern, text, re.DOTALL)
        return [block.strip() for block in code_blocks]

    def write_story_to_file(self, content, output_location):
        directory = os.path.dirname(output_location)
        os.makedirs(directory, exist_ok=True)
        try:
            final = self.extract_code_blocks(content)
            if isinstance(final, list) and final:
                content_to_write = final[0]
            else:
                content_to_write = final
            with open(output_location, "w", encoding="utf-8") as file:
                file.write(content_to_write)
        except Exception as e:
            print(f"An error occurred: {e}")
            return {"status": 401, "message": "Failed"}

        return {"status": 200, "message": "Success"}

    def write_output_to_file(self, content, output_location):
        with open(output_location, "w", encoding="utf-8") as file:
            file.write(content)

    def call_with_prompt(self, prompt_template_location, prompt, ai_to_use="gemini"):
        print(f"Using {ai_to_use} to generate.")
        base_prompt = self.load_from_file(prompt_template_location)
        if ai_to_use == "gemini":
            result = self.call_gemini(base_prompt + prompt)
        elif ai_to_use == "openai":
            result = self.call_openai_api(base_prompt + prompt)
        return {"status": 200, "message": "Success", "result": result}


from rich.console import Console
from rich.markdown import Markdown
from rich.panel import Panel


def print_md(md, width=80):
    md = Markdown(md)
    panel = Panel(
        md,
        title="[bold green]Start[/bold green]",
        border_style="bright_yellow",
        subtitle="[dim]End[/dim]",
    )
    console = Console(width=width, color_system="auto")
    console.print(panel)
