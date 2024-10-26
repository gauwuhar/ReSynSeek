import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms'; // Убедитесь, что это импортировано
import { RouterModule } from '@angular/router';
import { Router, NavigationEnd } from '@angular/router';

@Component({
  selector: 'app-user-settings-looking-for',
  standalone: true,
  imports: [CommonModule, FormsModule, RouterModule], // Добавьте FormsModule сюда
  templateUrl: './user-settings-looking-for.page.html',
  styleUrl: './user-settings-looking-for.page.sass',
})
export class UserSettingsLookingForComponent {
  showInputContainer = false; // Изначально скрыто
  newKeyword = ''; // Для нового ключевого слова
  keywords: string[] = []; // Массив для хранения ключевых слов
  showKeywordContainer = true; // Управление видимостью контейнера
  isEditing = false; // Состояние редактирования
  editIndex: number | null = null; // Индекс редактируемого ключевого слова

  // Переключение видимости поля ввода
  toggleInputContainer(): void {
    this.showInputContainer = true; // Всегда показываем поле ввода
    this.isEditing = false; // Убираем состояние редактирования
    this.newKeyword = ''; // Сбрасываем вводимое значение
  }

  // Добавление или обновление ключевого слова
  addKeyword(): void {
    const trimmedKeyword = this.newKeyword.trim();
    if (trimmedKeyword) {
      if (this.isEditing && this.editIndex !== null) {
        this.keywords[this.editIndex] = trimmedKeyword; // Обновление ключевого слова
      } else {
        this.keywords.push(trimmedKeyword); // Добавление нового ключевого слова
      }
      this.resetInput(); // Сброс поля ввода и состояния
    }
  }

  // Удаление ключевого слова
  removeKeyword(index: number): void {
    this.keywords.splice(index, 1); // Удаляем элемент по индексу
  }

  // Редактирование ключевого слова
  editKeyword(index: number): void {
    this.newKeyword = this.keywords[index];
    this.isEditing = true;
    this.editIndex = index;
    this.showInputContainer = true; // Показываем поле ввода при редактировании
  }

  // Очистка всех ключевых слов
  clearAllKeywords(): void {
    this.keywords = []; // Очищаем массив ключевых слов
  }

  // Сброс состояния ввода
  private resetInput(): void {
    this.newKeyword = '';
    this.showInputContainer = false; // Скрыть поле ввода после добавления
    this.isEditing = false;
    this.editIndex = null;
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
