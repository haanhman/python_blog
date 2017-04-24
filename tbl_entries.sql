CREATE TABLE IF NOT EXISTS `tbl_entries` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `title` varchar(255) NOT NULL,
  `description` text NOT NULL,
  `content` text NOT NULL,
  `create_date` int(11) NOT NULL,
  `edit_date` int(11) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=MyISAM  DEFAULT CHARSET=utf8 AUTO_INCREMENT=3 ;

--
-- Dumping data for table `tbl_entries`
--

INSERT INTO `tbl_entries` (`id`, `title`, `description`, `content`, `create_date`, `edit_date`) VALUES
(1, 'Tieu de', 'Mo ta bai viet so 1', 'noi dung bai viet', 1493025764, 1493025764),
(2, 'Subject 2', 'Mo ta bai viet so 2\r\nnoi dung la gi', 'content of entries', 1493025764, 1493025764);