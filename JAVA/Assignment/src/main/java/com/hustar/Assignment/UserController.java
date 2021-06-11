package com.hustar.Assignment;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.jdbc.core.JdbcTemplate;
import org.springframework.web.bind.annotation.*;

import java.sql.ResultSet;
import java.sql.SQLException;
import java.util.List;

@RestController
public class UserController {

    @Autowired
    JdbcTemplate jdbcTemplate;

    private static UserVO mapRow(ResultSet resultSet, int rowNum) throws SQLException {
        var user = new UserVO();
        user.id = resultSet.getInt("id");
        user.name = resultSet.getString("name");
        user.level = resultSet.getInt("level");

        return user;
    }

    @GetMapping("/users")
    public List<UserVO> getByLevel(@RequestParam (required = false) Integer level){
        String sql;

        if(level == null){ // 모든 사용자 조회
            sql = "SELECT * FROM users";
            List<UserVO> list = (List<UserVO>) jdbcTemplate.query(sql,
                    UserController::mapRow
            );
            return list;
        }
        else{ // 레벨로 필터링
            sql = "SELECT * FROM users WHERE level = ?";
            List<UserVO> list = (List<UserVO>) jdbcTemplate.query(sql,
                    UserController::mapRow,
                    new Object[]{level}
            );
            return list;
        }
    }

    @GetMapping("/users/{id}")
    public List<UserVO> getById(@PathVariable int id){
        String sql = "SELECT * FROM users WHERE id = ?";
        List<UserVO> list = (List<UserVO>) jdbcTemplate.query(sql,
                UserController::mapRow,
                id);
        return list;
    }

    // 사용자 추가
    @PostMapping("/users")
    public UserVO post(@RequestBody UserVO input){
        String sql = "INSERT INTO users (name, level) VALUES (?, ?)";
        jdbcTemplate.update(sql, new Object[]{input.name, input.level});

        UserVO result = jdbcTemplate.queryForObject(
                "SELECT * FROM users ORDER BY id DESC LIMIT 1",
                (resultSet, rowNum) -> {
                    var user = new UserVO();
                    user.id = resultSet.getInt("id");
                    user.name = resultSet.getString("name");
                    user.level = resultSet.getInt("level");

                    return user;
                });
        return result;
    }

    // 사용자 변경
    @PutMapping("/users/{id}")
    public UserVO update(@PathVariable int id, @RequestBody UserVO input){
        String sql = "UPDATE users SET name = ?, level = ? WHERE id = ?";
        jdbcTemplate.update(sql, new Object[] { input.name, input.level, id });

        UserVO result = jdbcTemplate.queryForObject(
                "SELECT * FROM users WHERE id = ?",
                UserController::mapRow,
                new Object[] { id }
        );

        return result;
    }

    @DeleteMapping("/users/{id}")
    public DelResultVO delete(@PathVariable int id) {
        String sql = "DELETE FROM users WHERE id = ?";
        jdbcTemplate.update(sql, new Object[] { id });
        var vo = new DelResultVO();
        vo.id = id;
        return vo;
    }
}
