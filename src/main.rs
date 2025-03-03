use liana::simplex::LinearProgram;

fn main() {
  // Example: Maximize 3x + 4y
  //          Subject to:
  //          x + 2y <= 8
  //          3x + 2y <= 12
  //          x, y >= 0

  let a = vec![vec![1.0, 2.0], vec![3.0, 2.0]];

  let b = vec![8.0, 12.0];

  let c = vec![3.0, 4.0];

  let lp = LinearProgram::new(a, b, c);

  match lp.solve() {
    Ok((solution, obj_val)) => {
      println!("Optimal solution:");
      for (i, &val) in solution.iter().enumerate() {
        println!("x_{} = {:.4}", i, val);
      }
      println!("Optimal objective value: {:.4}", obj_val);
    }
    Err(msg) => {
      println!("Error: {}", msg);
    }
  }
}
