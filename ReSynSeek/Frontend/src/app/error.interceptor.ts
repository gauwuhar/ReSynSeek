import { HttpInterceptorFn } from '@angular/common/http';
import { catchError, throwError } from 'rxjs';

// интресептор ошибок

export const errorInterceptor: HttpInterceptorFn = (req, next) => {
  return next(req).pipe(
    catchError((error)=>{
      // какие виды ошибок обрабытвает интерсептор ошибок
      if([401, 403].includes(error.status)) {
        console.log('Error found by me')
      }
    const e = error.error.message || error.statusText;
    console.log(e);
    return throwError(()=>error);
  }));
};
