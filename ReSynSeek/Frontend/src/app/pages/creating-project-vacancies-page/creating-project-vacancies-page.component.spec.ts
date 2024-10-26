import { ComponentFixture, TestBed } from '@angular/core/testing';

import { CreatingProjectVacanciesPageComponent } from './creating-project-vacancies-page.component';

describe('CreatingProjectVacanciesPageComponent', () => {
  let component: CreatingProjectVacanciesPageComponent;
  let fixture: ComponentFixture<CreatingProjectVacanciesPageComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [CreatingProjectVacanciesPageComponent]
    })
    .compileComponents();

    fixture = TestBed.createComponent(CreatingProjectVacanciesPageComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
