import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class AuthService {
  private apiUrl = 'http://127.0.0.1:5000';
  logged_in: boolean = false; // Инициализация со значением по умолчанию

  constructor(private http: HttpClient) { }

  checkAuth(): Observable<{ logged_in: boolean }> {
    return this.http.get<{ logged_in: boolean }>(`${this.apiUrl}/api/check_auth`);
  }
}
