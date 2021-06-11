package com.hustar.Assignment;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.CommandLineRunner;
import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.jdbc.core.JdbcTemplate;

@SpringBootApplication
public class AssignmentApplication implements CommandLineRunner {

	@Autowired
	JdbcTemplate jdbcTemplate;

	public static void main(String[] args) {
		SpringApplication.run(AssignmentApplication.class, args);
	}

	@Override
	public void run(String... args) throws Exception {
		// Create Users
		jdbcTemplate.execute("CREATE TABLE users (\n" +
				"  id SERIAL,\n" +
				"  name VARCHAR(255),\n" +
				"  level INT\n" +
				")");

		// Create Messages
		jdbcTemplate.execute("CREATE TABLE messages (\n" +
				"  id SERIAL,\n" +
				"  message VARCHAR(255),\n" +
				"  fromId int,\n" +
				"  toId int\n" +
				")");
	}
}
