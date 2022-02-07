from deep_translator import GoogleTranslator

async def translate(interaction, target):
    m = interaction.data["resolved"]["messages"][interaction.data['target_id']]
    content = m["content"]
    try:
        g = GoogleTranslator(source = "auto", target = target)
        result = g.translate(content)
    except Exception as e:
        with open("error.txt", "w") as f:
            f.write(traceback.format_exc())
        result = f"エラーが発生しました\n{e}"
    await interaction.send(embed = {
        "title": "translate",
        "fields": [
            {
                "name": "before",
                "value": content
            },
            {
                "name": "after",
                "value": result
            }
        ]
    })