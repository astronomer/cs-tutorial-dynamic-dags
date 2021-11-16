drop table if exists public.dag_config;
create table if not exists public.dag_config (
  dagid varchar,
  schedule varchar,
  query varchar
);

insert into public.dag_config (dagid, schedule, query)
values('dag_file_1', '@daily', 'select * from table1;')
;

insert into public.dag_config (dagid, schedule, query)
values('dag_file_2', '@weekly', 'select * from table2;')
;

insert into public.dag_config (dagid, schedule, query)
values('dag_file_3', '@monthly', 'select * from table3;')
;

select * from public.dag_config;