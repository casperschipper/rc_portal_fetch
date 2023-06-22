# Research Catalogue Portal Metadata export script

This is a script that allows you to export the metadata of your/a portal in the Research Catalogue.

To use this, you need Python3 and requests library.
If you also want to export portal internal data, add a secret.py file with the following contents:

```python
class Secret(object):
  username = 'yourusername'
  password = 'yourpassword'
```



