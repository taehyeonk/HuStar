package com.hustar.Assignment;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.jdbc.core.JdbcTemplate;
import org.springframework.web.bind.annotation.*;

import java.sql.ResultSet;
import java.sql.SQLException;
import java.util.List;

@RestController
public class MessageController {

    @Autowired
    JdbcTemplate jdbcTemplate;

    private static MessageVO mapRow(ResultSet resultSet, int rowNum) throws SQLException {
        var message = new MessageVO();
        message.id = resultSet.getInt("id");
        message.message = resultSet.getString("message");
        message.fromId = resultSet.getInt("fromId");
        message.from = resultSet.getString("from");
        message.toId = resultSet.getInt("toId");
        message.to = resultSet.getString("to");

        return message;
    }

    @GetMapping("/messages")
    public List<MessageVO> getAll(){
        String sql = "SELECT messages.id, messages.message, messages.fromId, nfrom.name AS \"from\", messages.toId, nto.name AS \"to\"\n" +
                "FROM messages\n" +
                "INNER JOIN users AS nfrom ON messages.fromid = nfrom.id\n" +
                "INNER JOIN users AS nto ON messages.toid = nto.id";

        List<MessageVO> list = (List<MessageVO>) jdbcTemplate.query(sql,
                MessageController::mapRow);

        return list;
    }

    @GetMapping("/messages/from/{id}")
    public List<MessageVO> getFromId(@PathVariable int id){
        String sql = "SELECT messages.id, messages.message, messages.fromId, nfrom.name AS \"from\", messages.toId, nto.name AS to\n" +
                "FROM messages\n" +
                "INNER JOIN users AS nfrom ON messages.fromid = nfrom.id\n" +
                "INNER JOIN users AS nto ON messages.toid = nto.id\n" +
                "WHERE messages.fromid = ?";

        List<MessageVO> list = (List<MessageVO>) jdbcTemplate.query(sql,
                MessageController::mapRow,
                id);

        return list;
    }

    @GetMapping("/messages/to/{id}")
    public List<MessageVO> getToId(@PathVariable int id){
        String sql = "SELECT messages.id, messages.message, messages.fromId, nfrom.name AS \"from\", messages.toId, nto.name AS to\n" +
                "FROM messages\n" +
                "INNER JOIN users AS nfrom ON messages.fromid = nfrom.id\n" +
                "INNER JOIN users AS nto ON messages.toid = nto.id\n" +
                "WHERE messages.toid = ?";

        List<MessageVO> list = (List<MessageVO>) jdbcTemplate.query(sql,
                MessageController::mapRow,
                id);

        return list;
    }

    @PostMapping("/messages")
    public MessageVO post(@RequestBody MessagePostVO input){
        String sql = "INSERT INTO messages (message, fromId, toId) VALUES (?, ?, ?)";
        jdbcTemplate.update(sql, new Object[]{input.message, input.fromId, input.toId});

        MessageVO result = jdbcTemplate.queryForObject(
                "SELECT messages.id, messages.message, messages.fromId, nfrom.name AS \"from\", messages.toId, nto.name AS to\n" +
                        "FROM messages\n" +
                        "INNER JOIN users AS nfrom ON messages.fromid = nfrom.id\n" +
                        "INNER JOIN users AS nto ON messages.toid = nto.id\n" +
                        "ORDER BY id DESC LIMIT 1",
                MessageController::mapRow);
        return result;
    }

    @PutMapping("/messages/{id}")
    public MessageVO put(@PathVariable int id, @RequestBody MessagePostVO input){
        String sql = "UPDATE messages SET message = ?, fromId = ?, toId = ? WHERE id = ?";
        jdbcTemplate.update(sql, new Object[] { input.message, input.fromId, input.toId, id });

        MessageVO result = jdbcTemplate.queryForObject(
                "SELECT messages.id, messages.message, messages.fromId, nfrom.name AS \"from\", messages.toId, nto.name AS to\n" +
                        "FROM messages\n" +
                        "INNER JOIN users AS nfrom ON messages.fromid = nfrom.id\n" +
                        "INNER JOIN users AS nto ON messages.toid = nto.id\n" +
                        "WHERE messages.id = ?",
                MessageController::mapRow,
                new Object[] { id }
        );

        return result;
    }

    @DeleteMapping("/messages/{id}")
    public DelResultVO delete(@PathVariable int id) {
        String sql = "DELETE FROM messages WHERE id = ?";
        jdbcTemplate.update(sql, new Object[] { id });
        var vo = new DelResultVO();
        vo.id = id;
        return vo;
    }
}
