import { RouterTestingModule } from '@angular/router/testing';
import { TestBed } from '@angular/core/testing';
import { HeaderComponent } from './header.component';

describe('HeaderComponent', () => {
  beforeEach(() => {
    TestBed.configureTestingModule({
      imports: [RouterTestingModule], // Добавьте RouterTestingModule для тестов
      declarations: [HeaderComponent]
    }).compileComponents();
  });

  // Ваши тесты здесь
});
