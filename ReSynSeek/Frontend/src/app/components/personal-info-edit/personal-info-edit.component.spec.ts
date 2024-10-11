import { ComponentFixture, TestBed } from '@angular/core/testing';

import { PersonalInfoEditComponent } from './personal-info-edit.component';

describe('PersonalInfoEditComponent', () => {
  let component: PersonalInfoEditComponent;
  let fixture: ComponentFixture<PersonalInfoEditComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [PersonalInfoEditComponent]
    })
    .compileComponents();

    fixture = TestBed.createComponent(PersonalInfoEditComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
