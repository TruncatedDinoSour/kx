# Registers

Kx uses the FASM assembly which has the following registers which Kx uses:

| Bits | Name   | Types                         | Use                                                                                                               |
| ---- | ------ | ----------------------------- | ----------------------------------------------------------------------------------------------------------------- |
| 8    |        | `u8`, `i8`, `char`, `bool`    |                                                                                                                   |
|      | `spl`  | -                             | Low byte of the stack pointer. Used for low-level stack manipulation.                                             |
|      | `bpl`  | -                             | Base pointer low byte. Used in the stack frame to access local variables and function arguments.                  |
|      | `sil`  | -                             | Source index low byte. Used in string and memory operations.                                                      |
|      | `dil`  | -                             | Destination index low byte. Used in string and memory operations.                                                 |
|      | `r8b`  |                               | General purpose.                                                                                                  |
|      | `r9b`  |                               | General purpose.                                                                                                  |
|      | `r10b` |                               | General purpose.                                                                                                  |
|      | `r11b` |                               | General purpose.                                                                                                  |
|      | `r12b` |                               | General purpose.                                                                                                  |
|      | `r13b` |                               | General purpose.                                                                                                  |
|      | `r14b` |                               | General purpose.                                                                                                  |
|      | `r15b` |                               | General purpose.                                                                                                  |
| 16   |        | `u16`, `i16`, `char16`        |                                                                                                                   |
|      | r8w    |                               | General purpose.                                                                                                  |
|      | r9w    |                               | General purpose.                                                                                                  |
|      | r10w   |                               | General purpose.                                                                                                  |
|      | r11w   |                               | General purpose.                                                                                                  |
|      | r12w   |                               | General purpose.                                                                                                  |
|      | r13w   |                               | General purpose.                                                                                                  |
|      | r14w   |                               | General purpose.                                                                                                  |
|      | r15w   |                               | General purpose.                                                                                                  |
| 32   |        | `u32`, `i32`, `f32`, `char32` |                                                                                                                   |
|      | r8d    |                               | General purpose.                                                                                                  |
|      | r9d    |                               | General purpose.                                                                                                  |
|      | r10d   |                               | General purpose.                                                                                                  |
|      | r11d   |                               | General purpose.                                                                                                  |
|      | r12d   |                               | General purpose.                                                                                                  |
|      | r13d   |                               | General purpose.                                                                                                  |
|      | r14d   |                               | General purpose.                                                                                                  |
|      | r15d   |                               | General purpose.                                                                                                  |
| 64   |        | `u64`, `i64`, `f64`           |                                                                                                                   |
|      | rax    |                               | Accumulator register. Used as a general purpose register and for function return values.                          |
|      | rcx    |                               | Counter register. Used in loops and as a general purpose register.                                                |
|      | rdx    |                               | Data register. Used for I/O operations, multiplication/division results and as a general purpose register.        |
|      | rbx    |                               | Base register. Used as a pointer to data (base pointer in data segment) and as a general-purpose register.        |
|      | rsp    | `any*`                        | Stack pointer register (points to the top of the stack). Used for function call management.                       |
|      | rbp    | `any*`                        | Base pointer register. Used to point to the base of the stack frame and in navigating frame-based data.           |
|      | rsi    |                               | Source index. Used for string and memory operations (source pointer) and as a general-purpose register.           |
|      | rdi    |                               | Destination index. Used for string and memory operations (destination pointer) and as a general-purpose register. |
|      | r8     |                               | General purpose.                                                                                                  |
|      | r9     |                               | General purpose.                                                                                                  |
|      | r10    |                               | General purpose register. Used for (usually) temporary data.                                                      |
|      | r11    |                               | General purpose register. Used for (usually) temporary data.                                                      |
|      | r12    |                               | General purpose register. Used as a calee-saved register which is preserved across function calls.                |
|      | r13    |                               | General purpose register. Used as a calee-saved register which is preserved across function calls.                |
|      | r14    |                               | General purpose register. Used as a calee-saved register which is preserved across function calls.                |
|      | r15    |                               | General purpose register. Used as a calee-saved register which is preserved across function calls.                |
