create database if not exists testdb;

SELECT `sys_config`.`variable`,
    `sys_config`.`value`,
    `sys_config`.`set_time`,
    `sys_config`.`set_by`
FROM `sys`.`sys_config`;

CREATE DATABASE testdb DEFAULT charset utf8 collate utf8_general_ci;

SELECT `maoyan`.`title`,
    `maoyan`.`actor`,
    `maoyan`.`time`
FROM `testdb`.`maoyan`;

use testdb;
# 把表改成utf-8
alter table testdb.maoyan  character set utf8;

# 把表中的某个字段改成utf-8
alter table testdb.maoyan change title title varchar(2000)  character set utf8;
alter table testdb.maoyan change actor actor varchar(2000)  character set utf8;
alter table testdb.maoyan change time time varchar(2000)  character set utf8;

DELETE FROM `testdb`.`maoyan`
WHERE title='英雄本色3';

