class JAVMovie:
    def __init__(self, args):
        if "title" in args.keys():
            self.title = args["title"]
        else:
            self.title = None
        if "jav_code" in args.keys():
            self.jav_code = args["jav_code"]
        else:
            self.jav_code = None
        if "tags" in args.keys():
            self.tags = args["tags"]
        else:
            self.tags = None
        if "studio_label" in args.keys():
            self.studio_label = args["studio_label"]
        else:
            self.studio_label = None
        if "release_date" in args.keys():
            self.release_date = args["release_date"]
        else:
            self.release_date = None
        if "image_url" in args.keys():
            self.image_url = args["image_url"]
        else:
            self.image_url = None
        if "content_id" in args.keys():
            self.content_id = args["content_id"]
        else:
            self.content_id = None

    def __str__(self):
        print("<JAVMovie " + self.jav_code + ">")

