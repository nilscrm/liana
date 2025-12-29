# Liana

Liana is a linear program solver written in [Vine](https://vine.dev/). It uses
the simplex method to solve linear programs.

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
let x = lp.new_var("x", 0.0, F32::inf);
let y = lp.new_var("y", 0.0, F32::inf);

lp.add_constraint(Constraint(x + 2.0 * y, Le(), 8.0 as Term));
lp.add_constraint(Constraint(3.0 * x + 2.0 * y, Le(), 12.0 as Term));

lp.set_objective(Objective::Maximize(3.0 * x + 4.0 * y));

let solution = lp.solve();
```

You can also run this example with

```bash
vine run liana/example.vi --lib liana/liana.vi
```

## Structure

- [`constraint.vi`](./liana/constraint.vi): Represents a single linear
  constraint
- [`example.vi`](./liana/example.vi): Contains the example linear program shown
  above
- [`linear_program`](./liana/linear_program.vi): Main struct to define linear
  programs
- [`simplex.vi`](./liana/simplex.vi): Contains the implementation of the simplex
  method for solving linear programs
- [`term.vi`](./liana/term.vi): Linear making up constraints and objective
  functions with a custom DSL
- [`variable.vi`](./liana/variable.vi): Variables used in terms
