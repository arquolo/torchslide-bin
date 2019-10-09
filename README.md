# TorchSlide
- Works only on Python-3.6
- Bundles all binaries from [ASAP](https://github.com/computationalpathologygroup/ASAP) to single package
- Provides array-like interface for `ASAP::MultiResolutionImage`

## Usage:

```python
import torchslide as ts

slide = ts.Image('test.svs')
shape: 'Tuple[int]' = slide.shape
scales: 'Tuple[int]' = slide.scales
image: np.ndarray = slide[:2048, :2048]  # get numpy.ndarray
```
