# FastPy

FastPy is a statically typed programming language with pythonic syntax.

## About

FastPy is a new general purpose, multi-paradigm, high performance, statically typed programming language which have
pytonic intuitive syntax.

## Examples

- ["Hello, World"](examples/hello_world.fpy) program:

```python
# Just a comment :D

log('Hello, World!')  # print hello world
```

- ["Far Future"](examples/far_future.fpy) program:

```python
interface Car:
    public:
        fun __init__(name: str, weight: int): ...
		
		
        @property
        fun brand() -> str: ...
			
		
        @property
        fun name() -> str: ...
			
			
        @property
        fun weight() -> int: ...
		

class Tesla(Car): # Car implementation
    private:
        __name: str
        __weight: int
    public:
        fun __init__(name: str, weight: int):
            __name = name
            __weight = weight
		
		
        @property
        fun brand() -> str:
            return 'Tesla'
			
		
        @property
        fun name() -> str:
            return __name
			
			
        @property
        fun weight() -> int:
            return __weight



fun car_factory(car_brand: str, name: str, weight: int) -> Car:
    match car_brand:
        case "Tesla":
            return Tesla(name, weight)
        default:
            return null


some_car: Car = car_factory("Tesla", "Model X", 2301) 
log(some_car.name) # Model X
log(some_car.weight) # 2301
```

*\*For more samples, see [examples directory](examples).*

## Features

- Transpailable to C++. Therefore, compiled. Therefore, fast
- Easy intuitive syntax, similar to Python
- Statically typed
- Easy expandable
- Flexible, you can customize it for yourself or completely rewrite each component
- Built-in logging system

## Customizing

That language built in such a way as to support customizing at every stage of transpiling or interpreting. For more
info, see [customizing doc file](docs/Customizing.md).

## Highlighting

To enable syntax highlighting, see [highlighting doc file](docs/Highlighting.md).

## Licence

FastPy uses the MIT license. See the bundled [LICENSE](LICENSE) file for details.
