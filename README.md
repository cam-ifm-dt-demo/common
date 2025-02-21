# Common modules for the DT application

To install the `common` module as a dependency in another package, use:

```bash
uv add git+https://github.com/cam-ifm-dt-demo/common.git
```

To update the other package when the `common` module is modified:

```bash
uv sync -P cam_ifm_dt_demo_common
```

You will need to re-run this for every package that imports the `common` module, every time this package is modified.
