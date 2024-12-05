import { Component, OnInit } from '@angular/core';
import { RouterModule, Router } from '@angular/router';
import { FormsModule } from '@angular/forms';
import { UserService } from '../../../services/user.service';

@Component({
  selector: 'app-profile',
  standalone: true,
  imports: [
    RouterModule,
    FormsModule // Включите FormsModule здесь, если это необходимо
  ],
  templateUrl: './profile.page.html',
  styleUrls: ['./profile.page.sass']
})
export class ProfileComponent implements OnInit {
  userId: string | null = '';
  fullName: string | null = ''; // Переменная для имени
  email: string | null = ''; // Переменная для почты

  constructor(private userService: UserService, private router: Router) {}

  ngOnInit(): void {
    this.userId = '9500821b-c0f3-4dbc-92e1-00e111069ac5'; // Получение ID сессии
    this.loadUserProfile(); // Загрузка данных профиля
  }

  async loadUserProfile() {
    try {
      // Передаем userId в метод получения профиля
      const profile = await this.userService.getUserProfile(this.userId!);
      this.fullName = profile.full_name; // Сохранение имени
      this.email = profile.email; // Сохранение почты
    } catch (error) {
      console.error('Ошибка при загрузке профиля пользователя', error);
    }
  }

  async handleLogout(event: Event) {
    event.preventDefault(); // Предотвратить стандартную отправку формы
    console.log('Current session ID:', this.userId); // Логирование userId
    try {
      const response = await this.userService.logout(this.userId!); // Вызов метода logout
      console.log('Logout successful!', response);
      this.router.navigate(['/login']); // Перенаправление на страницу логина
    } catch (error) {
      console.error('Logout failed', error);
    }
  }
}

