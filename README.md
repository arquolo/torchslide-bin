# Wrapper for [ASAP](https://github.com/computationalpathologygroup/ASAP)

- Bundles all libraries required for ASAP to single package.
- Provides array-like interface for `ASAP::MultiResolutionImage`

## Usage:

```python
import mir

with mir.open('test.svs') as image:
    shape = image.shape
    scales = image.scales
    patch = image[:2048, :2048]  # get numpy.ndarray
```
