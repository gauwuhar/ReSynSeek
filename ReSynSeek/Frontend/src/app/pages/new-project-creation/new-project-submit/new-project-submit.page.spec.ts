import { ComponentFixture, TestBed } from '@angular/core/testing';

import { NewProjectSubmitComponent } from './new-project-submit.page';

describe('NewProjectSubmitComponent', () => {
  let component: NewProjectSubmitComponent;
  let fixture: ComponentFixture<NewProjectSubmitComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [NewProjectSubmitComponent]
    })
    .compileComponents();

    fixture = TestBed.createComponent(NewProjectSubmitComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
