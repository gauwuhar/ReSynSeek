import { Component } from '@angular/core';
import { Router, RouterModule } from '@angular/router';
import { UserService } from '../../../services/user.service';
import { FormsModule } from '@angular/forms';
import { CommonModule } from '@angular/common';

@Component({
  selector: 'app-signup',
  standalone: true,
  imports: [RouterModule, FormsModule, CommonModule], // Import CommonModule here
  templateUrl: './signup.page.html',
  styleUrls: ['./signup.page.sass']
})
export class SignupComponent {
  agreeToTerms = false;
  fullName = '';
  email = '';
  password = '';
  confirmPassword = '';
  errorMessage = ''; // To hold error messages for user feedback

  constructor(private userService: UserService, private router: Router) {}

  async registerUser() {
    if (!this.agreeToTerms || this.password !== this.confirmPassword) {
      alert("Please ensure all fields are filled correctly and that passwords match.");
      return;
    }

    const user = {
      fullName: this.fullName,
      email: this.email,
      password: this.password
    };

    try {
      await this.userService.registerUser(user);
      alert("Registration successful!"); // Provide feedback on success
      this.router.navigate(['/scientific-interests-page']); // Navigate after successful registration
    } catch (error) {
      this.errorMessage = "Registration failed. Please try again."; // Set error message
      console.error(error); // Log the error for debugging
    }
  }
}
