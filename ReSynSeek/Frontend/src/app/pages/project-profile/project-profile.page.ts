import { Component } from '@angular/core';
import { Router, NavigationEnd } from '@angular/router';
import { RouterModule } from '@angular/router';

@Component({
  selector: 'app-project-profile',
  standalone: true,
  imports: [RouterModule],
  templateUrl: './project-profile.page.html',
  styleUrls: ['./project-profile.page.sass']
})
export class ProjectProfileComponent {
  // Тексты для смены на кнопке
  originalButtonText = 'Contact Us';
  contactInfo = `
    verycleverscientist667@gmail.com
    +8 800 555 35 35
    Los Santos, England, America
    t.me/sheisnotmylove
  `;

  // Переменная для отслеживания состояния
  isContactVisible = false;

  // Функция для смены текста кнопки
  toggleContactInfo() {
    this.isContactVisible = !this.isContactVisible;
  }

  // Метод для получения текущего текста на кнопке
  getCurrentButtonText() {
    return this.isContactVisible ? this.contactInfo : this.originalButtonText;
  }
  constructor(private router: Router) {
    this.router.events.subscribe(event => {
      if (event instanceof NavigationEnd) {
        const fragment = this.router.parseUrl(this.router.url).fragment;
        if (fragment) {
          document.getElementById(fragment)?.scrollIntoView({ behavior: 'smooth' });
        }
      }
    });
  }
}
