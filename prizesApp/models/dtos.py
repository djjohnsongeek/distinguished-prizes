from prizesApp.models.database import Post

class PostModel:
    end_block = '}'

    def __init__(self, dbModel: Post):
        self.id = dbModel.id
        self.title = dbModel.title
        self.raw_content = dbModel.content
        self.like_count = dbModel.likes
        self.dislike_count = dbModel.dislikes
        self.parsed_content = self.parse_content(self.raw_content)

    def parse_content(self, raw_content: str) -> []:
        parsed_content = []
        block_content = ""
        for c in raw_content:
            if c == self.end_block:
                parsed_content.append(block_content)
                block_content = ""
            else:
                block_content += c

        if block_content != "":
            parsed_content.append(block_content)

        print(parsed_content)

        return parsed_content