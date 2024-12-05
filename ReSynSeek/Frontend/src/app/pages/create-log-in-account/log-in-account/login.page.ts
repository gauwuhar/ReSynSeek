import { Component } from '@angular/core';
import { RouterModule, Router } from '@angular/router';
import { FormsModule } from '@angular/forms'; // Import FormsModule
import { UserService } from '../../../services/user.service';

@Component({
  selector: 'app-login',
  standalone: true,
  imports: [
    RouterModule,
    FormsModule // Include FormsModule here
  ],
  templateUrl: './login.page.html',
  styleUrls: ['./login.page.sass']
})
export class LoginComponent {
  email: string = '';
  password: string = '';

  constructor(private userService: UserService, private router: Router) {}

  async handleLogin(event: Event) {
    event.preventDefault();
    try {
      const response = await this.userService.login(this.email, this.password);
      console.log('Login successful!', response);
      this.router.navigate(['/projects-feed-page']);
    } catch (error) {
      console.error('Login failed', error);
    }
  }
}
