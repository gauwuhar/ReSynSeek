import { Component } from '@angular/core';
import { RouterModule } from '@angular/router';

@Component({
  selector: 'app-header',
  standalone: true,
  imports: [RouterModule],
  templateUrl: './header.component.html',
  styleUrls: ['./header.component.sass']
})
export class HeaderComponent {
  isLogin = false;
  languages: { [key: string]: string } = {
    "English": "assets/icons/english-flag.png",
    "Русский": "assets/icons/russian-flag.png",
    "Қазақша": "assets/icons/kazakh-flag.svg"
  };

  selectedLanguage: string = 'English';
  dropdownOpen: boolean = false;

  toggleDropdown(): void {
    this.dropdownOpen = !this.dropdownOpen;
  }

  selectLanguage(language: string): void {
    this.selectedLanguage = language;
    this.dropdownOpen = false;
  }

  get availableLanguages(): string[] {
    return Object.keys(this.languages).filter(lang => lang !== this.selectedLanguage);
  }
}