import { ComponentFixture, TestBed } from '@angular/core/testing';

import { PersonalInfoEditPage } from './personal-info-edit.page';

describe('PersonalInfoEditPage', () => {
  let component: PersonalInfoEditPage;
  let fixture: ComponentFixture<PersonalInfoEditPage>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [PersonalInfoEditPage]
    })
    .compileComponents();

    fixture = TestBed.createComponent(PersonalInfoEditPage);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
