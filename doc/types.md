# Types

The Kx type system works on how registers work. Here is a list of all types Kx supports:

| Type     | Size     | Structure                                          | Bounds                                                  | Description                                                                         |
| -------- | -------- | -------------------------------------------------- | ------------------------------------------------------- | ----------------------------------------------------------------------------------- |
| `u8`     | 8 bits.  | 1 byte.                                            | [0; 255]                                                | An unsigned 8-bit integer.                                                          |
| `i8`     | 8 bits.  | 1 sign bit followed by 7 bits.                     | [-127; 127]                                             | A signed 8-bit integer.                                                             |
| `char`   | 8 bits.  | 1 byte.                                            | [0; 255]                                                | An unsigned 8-bit integer used for storing ASCII characters. Alias to `u8`.         |
| `bool`   | 8 bits.  | 1 byte.                                            | [0; 1]                                                  | An unsigned 8-bit integer which is always ensured to be either 0 or 1.              |
| `u16`    | 16 bits. | 2 bytes.                                           | [0; 65535]                                              | An unsigned 16-bit integer.                                                         |
| `i16`    | 16 bits. | 1 sign bit followed by 15 bits.                    | [-32,768; 32,767]                                       | A signed 16-bit integer.                                                            |
| `char16` | 16 bits. | 2 bytes.                                           | [0; 65535]                                              | An unsigned 16-bit integer used to represent UTF-16 data.                           |
| `u32`    | 32 bits. | 4 bytes.                                           | [0; 4294967295]                                         | An unsigned 32-bit integer.                                                         |
| `i32`    | 32 bits. | 1 sign bit followed by 31 bits.                    | [-2,147,483,648; 2,147,483,647]                         | A signed 32-bit integer.                                                            |
| `f32`    | 32 bits. | 1 sign bit, 8 bit exponent, and 23 bits mantissa.  | [1.18E-38; 3.4E+38]                                     | An always-signed 32-bit floating-point integer with up to 7 digits of precision.    |
| `char32` | 32 bits. | 4 bytes.                                           | [0; 65535]                                              | An unsigned 32-bit integer used to represent UTF-32 data.                           |
| `u64`    | 64 bits. | 8 bytes.                                           | [0; 18446744073709551615]                               | An unsigned 64-bit integer.                                                         |
| `i32`    | 64 bits. | 1 sign bit followed by 63 bits.                    | [-9,223,372,036,854,775,808; 9,223,372,036,854,775,807] | A signed 64-bit integer.                                                            |
| `f64`    | 64 bits. | 1 sign bit, 11 bit exponent, and 52 bits mantissa. | [2.23E-308; 1.8E+308]                                   | An always-signed 64-bit floating-point integer with up to 15 digits of precision.   |
| `ptr`    | -        | -                                                  | -                                                       | Pointer type depending on the platform. It is an alias to one of the integer types. |
| `any`    | -        | -                                                  | -                                                       | Any or no type.                                                                     |

## Qualifiers

Qualifiers extend a type. They might change how can it be changed, allocated and used.

| Qualifier | Description                                                              |
| --------- | ------------------------------------------------------------------------ |
| `const`   | Marks the value as constant.                                             |
| `static`  | Allocates the value on the stack. Value has to be known at compile time. |

## Casting

Any type can be cast to its higher-bit type, meaning you may cast a `u8` to a `u16` with no problem, although,
converting from `u16` to `u8` may cause overflow and should be discouraged unless it is explicit. You may cast
to and from any type if the variable type is `any` or any of its variants.

Casting is simple:

    (type)var

Where `type` is the target type and `var` is the variable you're casting.

## Pointers

Just like in C, Kx has a pointer system, where you can create and dereference pointers:

-   `type*` - Type: Pointer which holds data of a certain type.
-   `&var` - Create a pointer pointing to the variable.
-   `*var` - Dereference the pointer stored in `var`.

## Arrays

You can have fixed-size and dynamic arrays in Kx as follows:

    type var[n] = [
        ...
    ];

If `n` is supplied there is a static-size array allocated on the stack. You
may omit `n` if all values are known at compile time.

If you have something like this:

    type var[] = [
        ...
    ];

The array is assumed to be dynamic and values will get filled in at run time, the benifit
