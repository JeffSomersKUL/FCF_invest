def inject_config():
    from flask import current_app as app

    filtered_config = {
        k: v for k, v in app.config.items() if k.startswith("MY_")
    }
    return dict(config=filtered_config)
