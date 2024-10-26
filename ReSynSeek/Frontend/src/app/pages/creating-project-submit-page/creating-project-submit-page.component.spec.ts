import { ComponentFixture, TestBed } from '@angular/core/testing';

import { CreatingProjectSubmitPageComponent } from './creating-project-submit-page.component';

describe('CreatingProjectSubmitPageComponent', () => {
  let component: CreatingProjectSubmitPageComponent;
  let fixture: ComponentFixture<CreatingProjectSubmitPageComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [CreatingProjectSubmitPageComponent]
    })
    .compileComponents();

    fixture = TestBed.createComponent(CreatingProjectSubmitPageComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
