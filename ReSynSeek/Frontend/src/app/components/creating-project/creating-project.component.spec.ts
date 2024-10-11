import { ComponentFixture, TestBed } from '@angular/core/testing';

import { CreatingProjectComponent } from './creating-project.component';

describe('CreatingProjectComponent', () => {
  let component: CreatingProjectComponent;
  let fixture: ComponentFixture<CreatingProjectComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [CreatingProjectComponent]
    })
    .compileComponents();

    fixture = TestBed.createComponent(CreatingProjectComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
