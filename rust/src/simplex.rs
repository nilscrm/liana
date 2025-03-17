use core::fmt;

/// Represents a linear programming problem in tableau form
#[derive(Clone, Debug)]
struct Tableau {
  /// The tableau matrix. The last column is the constants column (b).
  /// The last row is the objective function row (z).
  matrix: Vec<Vec<f64>>,
  /// Number of original variables (excluding slack/surplus variables)
  num_original_vars: usize,
  /// Maps the basic variable indices to their row indices in the tableau
  basic_vars: Vec<usize>,
}

impl Tableau {
  /// Create a new tableau for a standard form linear programming problem:
  /// Maximize z = c^T x
  /// Subject to Ax <= b
  ///            x >= 0
  ///
  /// # Arguments
  /// * `a` - The constraint coefficients matrix
  /// * `b` - The constraint right-hand sides
  /// * `c` - The objective function coefficients
  pub fn new(a: &Vec<Vec<f64>>, b: &Vec<f64>, c: &Vec<f64>) -> Result<Self, &'static str> {
    let num_constraints = a.len();
    if num_constraints == 0 {
      return Err("No constraints provided");
    }

    let num_vars = a[0].len();
    if num_vars == 0 {
      return Err("No variables in constraints");
    }

    // Verify dimensions
    if b.len() != num_constraints {
      return Err("Constraint count mismatch between A and b");
    }

    if c.len() != num_vars {
      return Err("Variable count mismatch between A and c");
    }

    // Check that all constraint rows have the same length
    for row in a {
      if row.len() != num_vars {
        return Err("Inconsistent number of variables in constraints");
      }
    }

    // Check that all b values are non-negative (for initial BFS)
    for &val in b {
      if val < 0.0 {
        return Err("All b values must be non-negative for standard form");
      }
    }

    // Initialize the tableau matrix
    let mut matrix = Vec::with_capacity(num_constraints + 1);

    // Add constraint rows
    for i in 0..num_constraints {
      // Columns for vars, slack variables and rhs.
      let mut row = Vec::with_capacity(num_vars + num_constraints + 1);

      // Add original variables
      for j in 0..num_vars {
        row.push(a[i][j]);
      }

      // Add slack variables
      for j in 0..num_constraints {
        row.push(if i == j { 1.0 } else { 0.0 });
      }

      // Add RHS
      row.push(b[i]);

      matrix.push(row);
    }

    // Add objective function row
    let mut obj_row = Vec::with_capacity(num_vars + num_constraints + 1);

    // Add original variables with negated objective coefficients
    // Represents equation `c*x - obj_val = 0`
    for &coef in c {
      obj_row.push(-coef);
    }

    // Add slack variables (0 coefficients)
    for _ in 0..num_constraints {
      obj_row.push(0.0);
    }

    // Add RHS for objective (initially 0)
    obj_row.push(0.0);

    matrix.push(obj_row);

    // Initialize basic variables (initially the slack variables)
    let basic_vars = (num_vars..(num_vars + num_constraints)).collect();

    Ok(Tableau { matrix, num_original_vars: num_vars, basic_vars })
  }

  /// Find the entering variable index using the most negative coefficient rule
  fn find_entering_var(&self) -> Option<usize> {
    let obj_row = self.matrix.last().unwrap();
    let num_cols = obj_row.len() - 1; // Exclude RHS

    let mut min_coef = 0.0;
    let mut entering_var = None;

    for j in 0..num_cols {
      if obj_row[j] < min_coef {
        min_coef = obj_row[j];
        entering_var = Some(j);
      }
    }

    entering_var
  }

  /// Find the leaving variable index using the minimum ratio test
  fn find_leaving_var(&self, entering_var: usize) -> Option<usize> {
    let num_rows = self.matrix.len() - 1; // Exclude objective row

    let mut min_ratio = f64::INFINITY;
    let mut leaving_row = None;

    for i in 0..num_rows {
      let coef = self.matrix[i][entering_var];

      // Skip if coefficient is not positive
      if coef <= 0.0 {
        continue;
      }

      let ratio = self.matrix[i].last().unwrap() / coef;

      if ratio < min_ratio {
        min_ratio = ratio;
        leaving_row = Some(i);
      }
    }

    leaving_row
  }

  /// Perform a pivot operation
  fn pivot(&mut self, leaving_row: usize, entering_var: usize) {
    let num_rows = self.matrix.len();
    let num_cols = self.matrix[0].len();

    // Get the pivot element
    let pivot_element = self.matrix[leaving_row][entering_var];

    // Scale the pivot row
    for j in 0..num_cols {
      self.matrix[leaving_row][j] /= pivot_element;
    }

    // Update all other rows
    for i in 0..num_rows {
      if i != leaving_row {
        let factor = self.matrix[i][entering_var];

        for j in 0..num_cols {
          self.matrix[i][j] -= factor * self.matrix[leaving_row][j];
        }
      }
    }

    // Update the basic variable at the leaving row
    self.basic_vars[leaving_row] = entering_var;
  }

  /// Run the simplex method to solve the linear program
  pub fn solve(&mut self) -> Result<(Vec<f64>, f64), &'static str> {
    let num_rows = self.matrix.len() - 1; // Exclude objective row

    // Main simplex loop
    loop {
      // Find the entering variable
      let entering_var = match self.find_entering_var() {
        Some(var) => var,
        None => break, // Optimal solution found
      };

      println!("entering_var: {entering_var}");

      // Find the leaving variable
      let leaving_row = match self.find_leaving_var(entering_var) {
        Some(row) => row,
        None => return Err("Problem is unbounded"),
      };

      println!("leaving_row: {leaving_row}");

      // Perform the pivot
      self.pivot(leaving_row, entering_var);

      println!("{}", self);
    }

    // Extract the solution
    let mut solution = vec![0.0; self.num_original_vars];

    for i in 0..num_rows {
      let basic_var = self.basic_vars[i];

      if basic_var < self.num_original_vars {
        solution[basic_var] = *self.matrix[i].last().unwrap();
      }
    }

    // Extract the objective value (negative of the last element in the objective row)
    let objective_value = self.matrix.last().unwrap().last().unwrap();

    Ok((solution, *objective_value))
  }
}

impl fmt::Display for Tableau {
  fn fmt(&self, f: &mut fmt::Formatter) -> fmt::Result {
    let num_rows = self.matrix.len();
    let num_cols = self.matrix[0].len();

    for i in 0..num_rows {
      for j in 0..num_cols {
        write!(f, "{:10.4} ", self.matrix[i][j])?;
      }

      if i < num_rows - 1 {
        write!(f, "| x_{} = {:.4}", self.basic_vars[i], self.matrix[i].last().unwrap())?;
      } else {
        write!(f, "| z = {:.4}", -self.matrix[i].last().unwrap())?;
      }

      writeln!(f)?;
    }

    Ok(())
  }
}

/// A linear program in standard form
pub struct LinearProgram {
  /// Constraint coefficients
  a: Vec<Vec<f64>>,
  /// Right-hand side values
  b: Vec<f64>,
  /// Objective function coefficients
  c: Vec<f64>,
}

impl LinearProgram {
  /// Create a new linear program in standard form:
  /// Maximize c^T x
  /// Subject to Ax <= b
  ///            x >= 0
  pub fn new(a: Vec<Vec<f64>>, b: Vec<f64>, c: Vec<f64>) -> Self {
    LinearProgram { a, b, c }
  }

  /// Solve the linear program using the simplex method
  pub fn solve(&self) -> Result<(Vec<f64>, f64), &'static str> {
    let mut tableau = Tableau::new(&self.a, &self.b, &self.c)?;
    tableau.solve()
  }
}

// Test module
#[cfg(test)]
mod tests {
  use super::*;

  #[test]
  fn test_simple_lp() {
    // Maximize 3x + 4y
    // Subject to:
    // x + 2y <= 8
    // 3x + 2y <= 12
    // x, y >= 0

    let a = vec![vec![1.0, 2.0], vec![3.0, 2.0]];

    let b = vec![8.0, 12.0];

    let c = vec![3.0, 4.0];

    let lp = LinearProgram::new(a, b, c);

    match lp.solve() {
      Ok((solution, obj_val)) => {
        assert_eq!(solution.len(), 2);
        assert!((solution[0] - 2.0).abs() < 1e-6);
        assert!((solution[1] - 3.0).abs() < 1e-6);
        assert!((obj_val - 18.0).abs() < 1e-6);
      }
      Err(_) => {
        panic!("Test failed: could not solve the LP");
      }
    }
  }

  #[test]
  fn test_unbounded_lp() {
    // Maximize x + y
    // Subject to:
    // -x + y <= 1
    // x, y >= 0

    let a = vec![vec![-1.0, 1.0]];

    let b = vec![1.0];

    let c = vec![1.0, 1.0];

    let lp = LinearProgram::new(a, b, c);

    match lp.solve() {
      Ok(_) => {
        panic!("Test failed: LP should be unbounded");
      }
      Err(msg) => {
        assert_eq!(msg, "Problem is unbounded");
      }
    }
  }
}
