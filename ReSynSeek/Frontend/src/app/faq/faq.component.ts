import { Component, AfterViewInit } from '@angular/core';

@Component({
  selector: 'app-faq',
  standalone: true,
  imports: [],
  templateUrl: './faq.component.html',
  styleUrls: ['./faq.component.sass'] // исправлено на styleUrls
})
export class FAQComponent implements AfterViewInit {
  
  // Вызовем метод после инициализации
  ngAfterViewInit() {
    this.setupFAQ();
  }

  private setupFAQ() {
    // Получаем все радиокнопки и ответы
    const toggles = document.querySelectorAll<HTMLInputElement>('.faq__toggle');
    const answers = document.querySelectorAll<HTMLElement>('.faq__answer');

    // Функция для обновления отображения ответов
    const updateAnswers = () => {
      answers.forEach((answer, index) => {
        // Проверяем, выбран ли соответствующий вопрос
        const isChecked = toggles[index].checked;
        answer.style.display = isChecked ? 'block' : 'none';
      });
    };

    // Добавляем обработчики событий для каждой радиокнопки
    toggles.forEach((toggle) => {
      toggle.addEventListener('change', updateAnswers);
    });

    // Вызываем функцию для первоначального отображения ответов
    updateAnswers();
  }
}
