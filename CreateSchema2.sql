drop database if exists `TRUONGHOC2`;

-- create database
create database `TRUONGHOC2`;
use `TRUONGHOC2`;

-- create tables and set clustered index
create table `TRUONG`(
`MATR` varchar(20) not null,
`TENTR` varchar(50),
`DCHITR` varchar(50),
constraint primary key(`MATR`)
) ENGINE=InnoDB default charset = utf8;

create table `HS`(
`MAHS` varchar(20) not null,
`HO` varchar(20),
`TEN` varchar(50),
`CCCD` varchar(20),
`NTNS` date,
`DCHI_HS` varchar(50),
constraint primary key (`MAHS`)
) ENGINE=InnoDB default charset = utf8;

create table `HOC`(
`MATR` varchar(20) not null,
`MAHS` varchar(20) not null,
`NAMHOC` varchar(10),
`DIEMTB` float(4,1),
`XEPLOAI` varchar(2),
`KETQUA` varchar(3),
constraint primary key (`MATR`, `MAHS`, `NAMHOC`),
constraint foreign key(`MATR`) references `TRUONG`(`MATR`),
constraint foreign key(`MAHS`) references `HS`(`MAHS`)
) ENGINE=InnoDB default charset = utf8;

create index TENTR_index on `TRUONG`(`TENTR`);
create index NAMHOC_index on `HOC`(`NAMHOC`);
create index XEPLOAI_index on `HOC`(`XEPLOAI`);