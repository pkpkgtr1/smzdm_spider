-- phpMyAdmin SQL Dump
-- version 5.0.2
-- https://www.phpmyadmin.net/
--
-- 主机： localhost
-- 生成日期： 2020-11-27 10:15:43
-- 服务器版本： 5.7.29-log
-- PHP 版本： 7.3.17

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- 数据库： `smzdm`
--

-- --------------------------------------------------------

--
-- 表的结构 `ls_smzdm_massage`
--

CREATE TABLE `ls_smzdm_massage` (
  `id` int(20) NOT NULL COMMENT 'ID',
  `title` varchar(160) NOT NULL DEFAULT '' COMMENT '商品名称',
  `worthy` int(8) DEFAULT NULL COMMENT '值得买',
  `unworthy` int(8) DEFAULT NULL COMMENT '不值得买',
  `comment` int(8) DEFAULT NULL COMMENT '收藏',
  `collect` int(8) DEFAULT NULL COMMENT '评论',
  `price` varchar(50) NOT NULL COMMENT '价格',
  `mall` varchar(50) NOT NULL DEFAULT '' COMMENT '活动商家',
  `url` varchar(255) NOT NULL COMMENT '活动介绍页面地址',
  `jpg_url` varchar(255) NOT NULL COMMENT '商品图片地址',
  `tag` varchar(50) DEFAULT NULL COMMENT '标签（历史新低，手慢无）',
  `push` int(11) NOT NULL COMMENT '推送  0默认  1需要推送  2已推送',
  `time` timestamp NOT NULL COMMENT '商品时间戳',
  `create_time` datetime DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '创建时间'
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- --------------------------------------------------------

--
-- 替换视图以便查看 `smzdm_9_9`
-- （参见下面的实际视图）
--
CREATE TABLE `smzdm_9_9` (
`title` varchar(160)
,`price` varchar(50)
,`worthy` int(8)
,`mall` varchar(50)
,`push` int(11)
,`tag` varchar(50)
,`url` varchar(255)
,`jpg_url` varchar(255)
,`time` timestamp
);

-- --------------------------------------------------------

--
-- 表的结构 `smzdm_massage`
--

CREATE TABLE `smzdm_massage` (
  `id` int(20) NOT NULL COMMENT 'ID',
  `title` varchar(160) NOT NULL DEFAULT '' COMMENT '商品名称',
  `worthy` int(8) DEFAULT NULL COMMENT '值得买',
  `unworthy` int(8) DEFAULT NULL COMMENT '不值得买',
  `comment` int(8) DEFAULT NULL COMMENT '收藏',
  `collect` int(8) DEFAULT NULL COMMENT '评论',
  `price` varchar(50) NOT NULL COMMENT '价格',
  `mall` varchar(50) NOT NULL DEFAULT '' COMMENT '活动商家',
  `url` varchar(255) NOT NULL COMMENT '活动介绍页面地址',
  `jpg_url` varchar(255) NOT NULL COMMENT '商品图片地址',
  `tag` varchar(50) DEFAULT NULL COMMENT '标签（历史新低，手慢无）',
  `push` int(11) NOT NULL COMMENT '推送  0默认  1需要推送  2已推送',
  `time` timestamp NOT NULL COMMENT '商品时间戳',
  `create_time` datetime DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '创建时间'
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- --------------------------------------------------------

--
-- 替换视图以便查看 `smzdm_sd`
-- （参见下面的实际视图）
--
CREATE TABLE `smzdm_sd` (
`id` int(20)
,`title` varchar(160)
,`worthy` int(8)
,`unworthy` int(8)
,`comment` int(8)
,`collect` int(8)
,`price` varchar(50)
,`mall` varchar(50)
,`url` varchar(255)
,`jpg_url` varchar(255)
,`tag` varchar(50)
,`push` int(11)
,`time` timestamp
,`create_time` datetime
);

-- --------------------------------------------------------

--
-- 视图结构 `smzdm_9_9`
--
DROP TABLE IF EXISTS `smzdm_9_9`;

CREATE ALGORITHM=UNDEFINED DEFINER=`smzdm`@`%` SQL SECURITY DEFINER VIEW `smzdm_9_9`  AS  select `s`.`title` AS `title`,`s`.`price` AS `price`,`s`.`worthy` AS `worthy`,`s`.`mall` AS `mall`,`s`.`push` AS `push`,`s`.`tag` AS `tag`,`s`.`url` AS `url`,`s`.`jpg_url` AS `jpg_url`,`s`.`time` AS `time` from `smzdm_massage` `s` where ((`s`.`time` > '2020-06-30') and (`s`.`worthy` > 5) and (`s`.`push` < 2)) ;

-- --------------------------------------------------------

--
-- 视图结构 `smzdm_sd`
--
DROP TABLE IF EXISTS `smzdm_sd`;

CREATE ALGORITHM=UNDEFINED DEFINER=`smzdm`@`%` SQL SECURITY DEFINER VIEW `smzdm_sd`  AS  select `smzdm_massage`.`id` AS `id`,`smzdm_massage`.`title` AS `title`,`smzdm_massage`.`worthy` AS `worthy`,`smzdm_massage`.`unworthy` AS `unworthy`,`smzdm_massage`.`comment` AS `comment`,`smzdm_massage`.`collect` AS `collect`,`smzdm_massage`.`price` AS `price`,`smzdm_massage`.`mall` AS `mall`,`smzdm_massage`.`url` AS `url`,`smzdm_massage`.`jpg_url` AS `jpg_url`,`smzdm_massage`.`tag` AS `tag`,`smzdm_massage`.`push` AS `push`,`smzdm_massage`.`time` AS `time`,`smzdm_massage`.`create_time` AS `create_time` from `smzdm_massage` where ((`smzdm_massage`.`tag` = '历史低价') or (`smzdm_massage`.`tag` = '手慢无') or (`smzdm_massage`.`tag` like '%比上次发布低___%') or (`smzdm_massage`.`tag` = '近30日已发布新低') or (`smzdm_massage`.`tag` like '%京东好评率99%')) ;

--
-- 转储表的索引
--

--
-- 表的索引 `ls_smzdm_massage`
--
ALTER TABLE `ls_smzdm_massage`
  ADD PRIMARY KEY (`id`),
  ADD KEY `index_tag` (`tag`),
  ADD KEY `index_time` (`time`);

--
-- 表的索引 `smzdm_massage`
--
ALTER TABLE `smzdm_massage`
  ADD PRIMARY KEY (`id`),
  ADD KEY `index_tag` (`tag`),
  ADD KEY `index_time` (`time`);

--
-- 在导出的表使用AUTO_INCREMENT
--

--
-- 使用表AUTO_INCREMENT `ls_smzdm_massage`
--
ALTER TABLE `ls_smzdm_massage`
  MODIFY `id` int(20) NOT NULL AUTO_INCREMENT COMMENT 'ID';

--
-- 使用表AUTO_INCREMENT `smzdm_massage`
--
ALTER TABLE `smzdm_massage`
  MODIFY `id` int(20) NOT NULL AUTO_INCREMENT COMMENT 'ID';
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
