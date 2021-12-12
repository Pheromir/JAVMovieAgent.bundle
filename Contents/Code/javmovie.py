class JAVMovie:
    def __init__(self, args):
        if "title" is not None:
            self.title = args["title"]
        if "jav_code" in args.keys():
            self.jav_code = args["jav_code"]
        if "tags" in args.keys():
            self.tags = args["tags"]
        if "studio_label" in args.keys():
            self.studio_label = args["studio_label"]
        if "release_date" in args.keys():
            self.release_date = args["release_date"]
        if "image_url" in args.keys():
            self.image_url = args["image_url"]
        if "content_id" in args.keys():
            self.content_id = args["content_id"]

    def __str__(self):
        print("<JAVMovie " + self.jav_code + ">")

