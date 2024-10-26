import { ComponentFixture, TestBed } from '@angular/core/testing';

import { UserSettingsLookingForComponent } from './user-settings-looking-for.component';

describe('UserSettingsLookingForComponent', () => {
  let component: UserSettingsLookingForComponent;
  let fixture: ComponentFixture<UserSettingsLookingForComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [UserSettingsLookingForComponent]
    })
    .compileComponents();

    fixture = TestBed.createComponent(UserSettingsLookingForComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
