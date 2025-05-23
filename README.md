# Liana

Liana is a linear program solver written in [Vine](https://vine.dev/). It uses the simplex method to solve linear programs.

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
let lp = LinearProgram::new();
let x = lp.new_var("x");
let y = lp.new_var("y");

lp.add_constraint(Constraint::le(x + 2.0*y, 8.0 as Term));
lp.add_constraint(Constraint::le(3.0*x + 2.0*y, 12.0 as Term));

lp.set_objective(3.0*x + 4.0*y);
let (solution_value, solution) = lp.solve().unwrap();
```

You can also run this example with
```bash
vine run src/example.vi
```

## Structure
- [`constraint.vi`](./src/constraint.vi): Represents a single linear constraint
- [`example.vi`](./src/example.vi): Contains the example linear program shown above
- [`linear_program`](./src/linear_program.vi): Main struct to define linear programs
- [`simplex.vi`](./src/simplex.vi): Contains the implementation of the simplex method for solving linear programs
- [`term.vi`](./src/term.vi): Linear making up constraints and objective functions with a custom DSL
- [`variable.vi`](./src/variable.vi): Variables used in terms
