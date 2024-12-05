import { Component, OnInit } from '@angular/core';
import { RouterModule } from '@angular/router';
import { UserService } from '../../services/user.service';
import { CommonModule } from '@angular/common';

@Component({
  selector: 'app-following-page',
  standalone: true,
  imports: [RouterModule, CommonModule],
  templateUrl: './following-page.page.html',
  styleUrls: ['./following-page.page.sass']
})
export class FollowingPagePage implements OnInit {
  favorites: any[] = [];
  userId: string = '8d9cb596-b6eb-4c09-9faf-9802b2f8ad19'; // Замените на реальный userId

  constructor(private userService: UserService) {}

  ngOnInit(): void {
    this.loadFavorites();
  }

  loadFavorites(): void {
    this.userService.getFavorites(this.userId).subscribe(
      (data) => {
        this.favorites = data;
      },
      (error) => {
        console.error('Error fetching favorites:', error);
      }
    );
  }

  removeFavorite(projectId: string): void {
    this.userService.deleteFavorite(projectId).subscribe(
      () => {
        this.favorites = this.favorites.filter(f => f.project_id !== projectId);
      },
      (error) => {
        console.error('Error removing favorite:', error);
      }
    );
  }
}
