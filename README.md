# Liana

Liana is a linear program solver written in [Vine](https://vine.dev/). It uses the simplex method to solve linear programs in the standard form.

## Example
Solve the linear program
```math
\begin{align*}
\text{Maximize} \quad & 3x + 4y \\
\text{subject to} \quad & x + 2y \leq 8 \\
& 3x + 2y \leq 12 \\
& x, y \geq 0
\end{align*}
```

```rust
let cost_coefficients = [3.0, 4.0];
let a = [[1.0, 2.0],
        [3.0, 2.0]];
let right_hand_side = [8.0, 12.0];

let lp = Tableau::new(a, right_hand_side, cost_coefficients);
let (solution_value, solution) = lp.solve().unwrap();
```

You can also run this example with
```bash
vine run vine/example.vi
```

## Structure
- [`simplex.vi`](./vine/simplex.vi): Contains the implementation of the simplex method for solving linear programs
- [`example.vi`](./vine/example.vi): Contains the example linear program shown above
- [`rust/`](/rust/): Contains a Rust implementation for comparison
