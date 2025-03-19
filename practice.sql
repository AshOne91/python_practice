-- 데이터 베이스 삭제
drop database if exists student_db3;
-- 데이터 베이스 생성
create database if not exists student_db3; 
-- 테이블생성(학생)
	-- pk(id), name, age, kor, eng, math
create table if not exists student_db3.subjects(
	subject_id int auto_increment primary key,
    subject_name varchar(30) not null unique, -- 중복방지
    teacher varchar(10),
    credits int default 3 -- 학점 기본 값
);

create table if not exists student_db3.exam_scores(
	exam_scores_id int auto_increment primary key
    ,name varchar(100) not null
    ,exam_date date
    ,score int
    ,subject_id int -- fk(외래키)로 사용할 열
    -- ,foreign key(subject_id) references student_db3.subjects(subject_id)
);

insert into student_db3.subjects(subject_name,teacher,credits) values
('수학', '김선생',3),
('영어', '이선생',2),
('과학', '박선생',1)
;

insert into student_db3.exam_scores(name,exam_date,score,subject_id) values
('민수','2025-01-15',85,1),
('영희','2025-01-15',95,2),
('철수','2025-02-15',75,2),
('도영','2025-02-15',62,1),
('지훈','2025-02-15',83,2),
('도영','2025-02-15',83,5)
;
select * from student_db3.exam_scores;
-- -----------------------------------------------
-- 1. 수치함수  avg round max min sum
select
	avg(score) as avg_score,
    round(avg(score), 1) as round_score,
    max(score) as max_score,
    min(score) as min_score,
    sum(score) as sum_score
from student_db3.exam_scores;
-- 2. 문자열 함수
select
	-- 민수 math
    concat(name,' ',subject_id) as name_subject,
    -- 이름을 대문자로 변환
    upper(name) as upper_name,
    -- 년 월말 출력 2025-02
    substr(exam_date,1,7) as yearmonth
from student_db3.exam_scores;
-- 날자 함수
select
exam_date,
date_add(exam_date, interval 30 day) as next_date, -- 7일후
datediff(now(),exam_date) as day_since, -- 오늘과 차이
abs( datediff(now(),'2025-08-20') ) as d_day
from student_db3.exam_scores;
-- 조건함수
select
name,
score,
-- 90이상 A B C  if.. case when
if(score >=90, 'A', if(score>=80 ,'B','C')) as grade
from student_db3.exam_scores;

-- 조인
-- 매핑... 테이블간 공통 키를 기준으로 데이터를 매핑
-- inner join
	-- 두 테이블에서 조건에 맞는 데이터만 반환  교집합
-- 조인조건
	-- on: 조인 기준 열을 정함  a.id = b.id
    -- where : 추가 필터링
    
select
*
	-- es.name as student_name,
-- 	s.subject_name as subject_name
from student_db3.exam_scores as es 
	inner join student_db3.subjects s 
		on es.subject_id = s.subject_id;    
    
-- left join(left outer join)
	-- 왼쪽테이블의 모든 행을 포함, 오른쪽에서 일치하는 데이터가 없으면 null
select
*
	-- es.name as student_name,
-- 	s.subject_name as subject_name
from student_db3.exam_scores as es 
	left join student_db3.subjects s 
		on es.subject_id = s.subject_id; 
        
-- right join(right outer join) --> 사용 거의 안함
select
*
from student_db3.exam_scores as es 
	right join student_db3.subjects s 
		on es.subject_id = s.subject_id; 

-- full join(full outer join)
	-- 양쪽 모든 행을 포함, 일치하지 않으면 null
    -- left join + right join
select
*
from student_db3.exam_scores as es 
	left join student_db3.subjects s 
		on es.subject_id = s.subject_id
union    -- 두개의 결과를 합치면서 중복을 제거   union all 중복을 허용  
select
*  
from student_db3.exam_scores as es 
	right join student_db3.subjects s 
		on es.subject_id = s.subject_id        
;        
    
-- cross join
	-- 두 테이블의 모든 행을 조합(카티션 곱)
select
*
from student_db3.exam_scores as es 
	cross join student_db3.subjects s 		
;       -- 6 * 3  18

select
*
from student_db3.exam_scores as es, student_db3.subjects s 
where es.subject_id = s.subject_id		
;

-- teacher 가 김선생인 과목을 듣는 학생들 중에 점수가 80점 이상인 학생들
select 
	es.name as '학생명' -- stduent_name
    ,s.subject_name as '과목명' -- subject_name
    ,es.score '과목점수' -- as student_score    
from student_db3.exam_scores es 
	join student_db3.subjects s on es.subject_id = s.subject_id
where
	s.teacher ='김선생' and es.score >=80; 
    
    
with total_avg as(
select
avg(score) as all_avg
from student_db3.exam_scorescalc_avg
)
select
se.name, se.score
from student_db3.exam_scores se, total_avg ta
where se.score > ta.all_avg;