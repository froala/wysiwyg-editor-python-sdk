# Froala WYSIWYG Editor Python SDK

Easing the [Froala WYSIWYG HTML Editor](https://github.com/froala/wysiwyg-editor) server side integration in Python 2 and Python 3 projects.

## Dependencies

Python 2 or Python 3

[Wand ImageMagick binding for Python](http://docs.wand-py.org/en/0.4.3/)

## Installation

1. Clone this repo or download the zip.

2. Load `froala_editor` project directory in your project and import it.

3. To run Django examples:

 * Go to `django_examples` directory.
 * `$ python manage.py runserver` or `$ python3 manage.py runserver` to start a server at `http://localhost:8000/`.

4. To run Flask examples:

 * Go to `flask_examples` directory.
 * `$ export FLASK_APP=server.py`
 * `$ python -m flask run` or `$ python3 -m flask run` to start a server at `http://localhost:5000/`.

5. To run Pyramid examples:

 * Go to `pyramid_examples` directory.
 * `$ python server.py` or `$ python3 server.py` to start a server at `http://localhost:7000/`.

## Third Party Plugins
`common/index.html`
```python
<script src="static/bower_components/froala-wysiwyg-editor/js/third_party/embedly.min.js"></script>
<script src="static/bower_components/froala-wysiwyg-editor/js/third_party/spell_checker.min.js"></script>
<script src="static/bower_components/froala-wysiwyg-editor/js/third_party/font_awesome.min.js"></script>
<script type="text/javascript" src="https://cdnjs.cloudflare.com/ajax/libs/froala-editor/3.0.6/js/third_party/image_tui.min.js">
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/froala-editor/3.0.6/css/third_party/image_tui.min.css"></script>
```



## Import lib

```python
from froala_editor import File, Image, S3

from froala_editor import DjangoAdapter, FlaskAdapter, PyramidAdapter
# Or make a custom adapter for your framework.
```

## Documentation

 * [Official documentation](https://www.froala.com/wysiwyg-editor/docs/sdks/python)

## Help
- Found a bug or have some suggestions? Just submit an issue.
- Having trouble with your integration? [Contact Froala Support team](http://froala.dev/wysiwyg-editor/contact).


## License

The Froala WYSIWYG Editor Python SDK is licensed under MIT license. However, in order to use Froala WYSIWYG HTML Editor plugin you should purchase a license for it.

Froala Editor has [3 different licenses](http://froala.com/wysiwyg-editor/pricing) for commercial use.
For details please see [License Agreement](http://froala.com/wysiwyg-editor/terms).