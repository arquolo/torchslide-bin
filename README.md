# TorchSlide
- Works only on Python-3.6
- Bundles all binaries from [ASAP](https://github.com/computationalpathologygroup/ASAP) to single package
- Provides array-like interface for `ASAP::MultiResolutionImage`

## Usage:

```python
import torchslide as ts

with ts.open('test.svs') as slide:
    shape = slide.shape
    scales = slide.scales
    image = slide[:2048, :2048]  # get numpy.ndarray
```
