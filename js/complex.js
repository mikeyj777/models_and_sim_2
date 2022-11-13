export default class Complex_Number {
  constructor(real, complex) {
    this.real = real;
    this.complex = complex;
  }
  
  multiply(num2) {
    const r1 = this.real;
    const c1 = this.complex;
    const r2 = num2.real;
    const c2 = num2.complex;
    
    const r = r1*r2 - c1*c2;
    const c = r1*c2 + r2*c1;
    
    return new Complex_Number(r, c);
    
  }
  
  add(num2) {
    const r1 = this.real;
    const c1 = this.complex;
    const r2 = num2.real;
    const c2 = num2.complex;
    
    const r = r1 + r2;
    const c = c1 + c2;
    
    return new Complex_Number(r, c);
    
  }
  
  negative() {
    
    return new Complex_Number(-this.real, -this.complex);
    
  }
  
  subtract(num2) {
    
    return this.add(num2.negative());
    
  }
  
  inverse() {
    
    const a = this.real;
    const b = this.complex;
    
    const div = a**2 + b**2;
    
    const r = a / div;
    const c = -b / div;
    
    return new Complex_Number(r, c);
    
  }
  
  divide_by(num2) {
    
    const num2_inv = num2.inverse();
    return this.multiply(num2_inv);
    
  }
  
  pow(p) {
    
    if (p == 0) {
      return new Complex_Number(1,0);
    }

    let z = new Complex_Number(this.real, this.complex);

    if (p == 1) {
      return z;
    }
    
    if (p == -1) {
      return z.inverse();
    }
    
    let z_orig = new Complex_Number(this.real, this.complex);

    if (p <= 0) {
      z = z.inverse();
      z_orig = z_orig.inverse();
    }
    
    p = Math.abs(p)
    
    for (let i = 1; i < p; i++) {
      z = z.multiply(z_orig);
    }
    
    return z;
    
  }
  
}