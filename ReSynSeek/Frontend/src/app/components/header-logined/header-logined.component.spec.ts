import { ComponentFixture, TestBed } from '@angular/core/testing';

import { HeaderLoginedComponent } from './header-logined.component';

describe('HeaderLoginedComponent', () => {
  let component: HeaderLoginedComponent;
  let fixture: ComponentFixture<HeaderLoginedComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [HeaderLoginedComponent]
    })
    .compileComponents();

    fixture = TestBed.createComponent(HeaderLoginedComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
