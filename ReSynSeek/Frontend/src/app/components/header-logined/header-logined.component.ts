import { Component, ElementRef, ViewChild, HostListener, OnInit } from '@angular/core';
import { RouterModule } from '@angular/router';
import { AuthService } from '../../auth.service';

@Component({
  selector: 'app-header-logined',
  standalone: true,
  imports: [RouterModule],
  templateUrl: './header-logined.component.html',
  styleUrls: ['./header-logined.component.sass']
})
export class HeaderLoginedComponent implements OnInit {
  loggedIn: boolean = false;

  constructor(private authService: AuthService) {}

  ngOnInit(): void {
    this.authService.checkAuth().subscribe({
      next: (response: any) => { // Используем тип any
        this.loggedIn = response.logged_in; // Устанавливаем значение loggedIn на основе ответа
      },
      error: (error) => {
        console.error('Error checking authentication:', error); // Логируем ошибку
        this.loggedIn = false; // Устанавливаем loggedIn в false при ошибке
      }
    });
  }

  @ViewChild('userMenuToggle', { static: true }) userMenuToggle!: ElementRef;
  @ViewChild('userMenu', { static: true }) userMenu!: ElementRef;

  // Toggle user menu visibility
  toggleUserMenu(): void {
    this.userMenu.nativeElement.classList.toggle('user-menu--active');
  }

  // Listen for clicks outside the menu to close it
  @HostListener('document:click', ['$event'])
  closeUserMenu(event: MouseEvent): void {
    const target = event.target as HTMLElement;

    // Check if the click is outside the toggle and user menu
    if (!this.userMenuToggle.nativeElement.contains(target) && !this.userMenu.nativeElement.contains(target)) {
      this.userMenu.nativeElement.classList.remove('user-menu--active');
    }
  }
}
