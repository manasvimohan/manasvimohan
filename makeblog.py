import os
import core


instance = core.BookMaker()
myprompt = """
Write a blog with emojis on weight loss
"""
result = instance.call_openai_api(myprompt)
# core.print_md(result)


postName = "funnypeople"
folder_path = f"./src/content/blog/{postName}"
file_path = f"{folder_path}/{postName}.mdx"
os.makedirs(folder_path, exist_ok=True)

print(f"Folder structure '{folder_path}' created successfully.")

front_matter = """
---
title: "Chatbots: Revolutionizing Customer Support with LLMs and No-Code Builders 🚀🤖"
description: "Lorem ipsum dolor sit amet"
pubDate: "Jul 08 2022"
heroImage: "/blog-placeholder-3.jpg"
author: "Manasvi Mohan Sharma"
published: false
tags: "Chatbots, NoCode, LLM, AI, CustomerSupport, Innovation"
category: "Business, Workplace, Leadership"
---
"""

content = """

"""

with open(file_path, "w") as file:
    file.write(front_matter + result)
