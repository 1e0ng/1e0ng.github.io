---
comments: true
date: 2012-09-21 01:27:43
layout: post
slug: always-set-the-default-charset-for-db-table
title: Always Set the Default Charset for DB Table
wordpress_id: 1036
categories: articles
tags:
- Database
tags:
- Character Set
- MySQL
---

Today, I spent a long time to find a bug. I read code, but finally I found the cause is that the character set of table is not correct.

Record this to avoid making the same mistake. Character set should always be set while a table is created. For MySQL, the syntax is:

<!-- more -->
{% highlight sql linenos %}
CREATE TABLE tbl_name (column_list)
    [[DEFAULT] CHARACTER SET charset_name]
    [COLLATE collation_name]]

ALTER TABLE tbl_name
    [[DEFAULT] CHARACTER SET charset_name]
    [COLLATE collation_name]
{% endhighlight %}

Example:

``` sql   
CREATE TABLE t1 ( ... )
CHARACTER SET utf8;
```

Sometimes, you need to see what character set a database/table/column is, here is the solution I found at stackoverflow:


For Schemas:

``` sql    
SELECT default_character_set_name FROM information_schema.SCHEMATA S
WHERE schema_name = "schemaname";
```

For Tables:

``` sql    
SELECT CCSA.character_set_name FROM information_schema.`TABLES` T,
       information_schema.`COLLATION_CHARACTER_SET_APPLICABILITY` CCSA
WHERE CCSA.collation_name = T.table_collation
  AND T.table_schema = "schemaname"
  AND T.table_name = "tablename";
```

For Columns:

{% highlight sql linenos %}
SELECT character_set_name FROM information_schema.`COLUMNS` C
WHERE table_schema = "schemaname"
  AND table_name = "tablename"
  AND column_name = "columnname";
{% endhighlight %}
