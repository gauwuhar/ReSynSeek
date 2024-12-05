import { Injectable } from '@angular/core';
import { SubjectModel } from "../model/subject-model";
import { AboutMeModel } from "../model/about-me.model";
import { HttpClient } from "@angular/common/http";
import { BehaviorSubject, firstValueFrom, Observable } from "rxjs";
import { AuthService } from '../auth.service';  // Обновите путь в зависимости от вашей структуры папок


@Injectable({
  providedIn: 'root'
})
export class UserService {

  private apiUrl = 'http://127.0.0.1:5000';
  private currentSessionId: string | null = null;
  private currentUserSubject = new BehaviorSubject<any>(null); // Здесь можно хранить информацию о текущем пользователе


  constructor(private http: HttpClient,) {
    const user = JSON.parse(localStorage.getItem('currentUser') || 'null');
    this.currentUserSubject.next(user);
  }

  getScientificInterests(): SubjectModel[] {
    return [
      {
        id: '1',
        title: 'Project Management',
        url: '/assets/Project_Management.jpg'
      },
      {
        id: '2',
        title: 'Applied data analytics',
        url: '/assets/Applied_data_analytics.jpg'
      },
      {
        id: '3',
        title: 'Digital public administration',
        url: '/assets/Digital_public_administration.jpg'
      },
      {
        id: '4',
        title: 'Computer Science',
        url: '/assets/Computer_Science.jpg'
      },
      {
        id: '5',
        title: 'Software Engineering',
        url: '/assets/Software_Engineering.jpg'
      },
      {
        id: '6',
        title: 'Big Data Analysis',
        url: '/assets/Big_Data_Analysis.jpg'
      },
      {
        id: '7',
        title: 'Media Technologies',
        url: '/assets/Media_Technologies.jpg'
      },
      {
        id: '8',
        title: 'Mathematical and Computational Science',
        url: '/assets/Mathematical_and_Computational_Science.jpg'
      },
      {
        id: '9',
        title: 'Big Data in Healthcare',
        url: '/assets/Big_Data_in_Healthcare.jpg'
      },
      {
        id: '10',
        title: 'Cybersecurity',
        url: '/assets/Cybersecurity.jpg'
      },
      {
        id: '11',
        title: 'Smart Technologies',
        url: '/assets/Smart_Technologies.jpg'
      },
      {
        id: '12',
        title: 'Industrial Internet of Things',
        url: '/assets/Industrial_Internet_of_Things.jpg'
      },
      {
        id: '13',
        title: 'Electronic Engineering',
        url: '/assets/Electronic_Engineering.jpg'
      },
      {
        id: '14',
        title: 'IT Management',
        url: '/assets/IT_Management.jpg'
      },
      {
        id: '15',
        title: 'IT Entrepreneurship',
        url: '/assets/IT_Entrepreneurship.jpg'
      },
      {
        id: '16',
        title: 'AI Business',
        url: '/assets/AI_Business.jpg'
      },
      {
        id: '17',
        title: 'Digital Journalism',
        url: '/assets/Digital_Journalism.jpg'
      },
      {
        id: '18',
        title: 'Computer Science and Information Networks',
        url: '/assets/Computer_Scienc_and_Information_Networks.jpg'
      },
    ];
  };


  getCurrentUserId(): string | null {
    const currentUser = this.currentUserSubject.value;
    return currentUser ? currentUser.user_id : null; // Предполагается, что у пользователя есть поле user_id
  }

  saveInterests(interests: string[]): Observable<any> {
    return this.http.post(`${this.apiUrl}/api/save_interests`, {
      user_id: this.getCurrentUserId(), // Теперь этот метод существует
      interests: interests,
    });
  }


  getHelloWorld() {
    return firstValueFrom(this.http.get("${this.apiUrl}/api/data"))
  }

  async registerUser(user: { fullName: string, email: string, password: string }) {
    try {
      const response = await firstValueFrom(this.http.post(`${this.apiUrl}/register`, user));
      return response; // Return response for further use if needed
    } catch (error) {
      console.error("Registration failed:", error);
      throw error; // Rethrow the error to handle it in the component
    }
  }

  async login(email: string, password: string) {
    const loginData = { email, password };
    try {
      const response = await firstValueFrom(this.http.post<{ sessionId: string }>(`${this.apiUrl}/login`, loginData));
      this.setSessionId(response.sessionId); // Установка ID сессии после успешного входа
      return response; // Вернуть ответ для дальнейшего использования, если необходимо
    } catch (error) {
      console.error("Login failed:", error);
      throw error; // Повторное выбрасывание ошибки для обработки в компоненте
    }
  }

  setSessionId(sessionId: string) {
    localStorage.setItem('sessionId', sessionId); // Сохранение sessionId в локальном хранилище
    console.log('Session ID saved:', sessionId); // Логирование сохраненного sessionId
  }


  getSessionId(): string | null {
    return this.currentSessionId;
  }

  async logout(sessionId: string) {
    const logoutData = { session_id: sessionId };
    console.log('Sending logout data:', logoutData); // Логирование данных для отправки
    try {
      const response = await firstValueFrom(this.http.post(`${this.apiUrl}/logout`, logoutData));
      return response; // Вернуть ответ для дальнейшего использования, если необходимо
    } catch (error) {
      console.error("Logout failed:", error);
      throw error; // Повторно выбросить ошибку для обработки в компоненте
    }
  }


  checkAuth(): Observable<AuthService> {
    return this.http.get<AuthService>(`${this.apiUrl}/api/check_auth`);
  }

  async getUserProfile(userId: string): Promise<{ full_name: string; email: string }> {
    try {
      const response = await firstValueFrom(
        this.http.get<{full_name: string; email: string}>(`${this.apiUrl}/profile/${userId}`)
      );
      return response; // Вернуть данные профиля
    } catch (error) {
      console.error("Failed to fetch user profile:", error); // Логировать ошибку
      throw error; // Повторно выбросить ошибку для обработки в компоненте
    }
  }

  getFavorites(userId: string): Observable<any[]> {
    return this.http.get<any[]>(`${this.apiUrl}/profile-favorites/${userId}`); // Передаем userId в URL
  }

  deleteFavorite(projectId: string): Observable<void> {
    return this.http.delete<void>(`${this.apiUrl}/profile-favorites/delete/${projectId}`);
  }




  getAboutMe(): AboutMeModel {
    return {
      aboutMe: "Just a regular human trying to convince AI that I'm not a robot. Successfully aced CAPTCHA 10 times in a row.",
      scientificExperience: [
        "Master of turning coffee into code (self-proclaimed)",
        "Co-Founder of the 'Procrastinators Anonymous' club (we'll have our first meeting... eventually)",
        "Once debugged a program with sheer willpower and questionable keyboard smashing"
      ],
      working: ["Currently pretending to be productive while actually Googling 'funny coding memes'", 'asdasdasdasd some shit'],
      edSkills: ["Expert in pushing buttons and hoping something magical happens. Also, I can kind of code."],
      contacts: ["Carrier pigeon, smoke signals, or @funnycoder if you're tech-savvy."],
    }
  }
}
