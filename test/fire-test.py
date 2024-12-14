import fire


def hello(name="World", fuck="yes"):
    a = "Hello %s!" % name
    print(a)


def main(task, **kwargs):
    globals()[task](**kwargs)


if __name__ == "__main__":
    fire.Fire(main)
