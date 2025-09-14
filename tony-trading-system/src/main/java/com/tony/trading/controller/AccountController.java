package com.tony.trading.controller;

import com.tony.trading.model.AccountBalance;
import com.tony.trading.service.AccountService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.*;
import org.springframework.web.servlet.mvc.support.RedirectAttributes;

/**
 * 账户管理控制器
 */
@Controller
@RequestMapping("/account")
public class AccountController {

    private final AccountService accountService;

    @Autowired
    public AccountController(AccountService accountService) {
        this.accountService = accountService;
    }

    /**
     * 显示账户管理页面
     */
    @GetMapping
    public String showAccount(Model model) {
        AccountBalance accountBalance = accountService.getAccountBalance();
        model.addAttribute("accountBalance", accountBalance);
        return "account/manage";
    }

    /**
     * 重置账户
     */
    @PostMapping("/reset")
    public String resetAccount(@RequestParam("initialBalance") double initialBalance,
                              RedirectAttributes redirectAttributes) {
        try {
            if (initialBalance <= 0) {
                redirectAttributes.addFlashAttribute("error", "初始资金必须大于0");
                return "redirect:/account";
            }
            
            accountService.resetAccount(initialBalance);
            redirectAttributes.addFlashAttribute("success", "账户重置成功！初始资金：" + initialBalance + " U");
        } catch (Exception e) {
            redirectAttributes.addFlashAttribute("error", "重置账户失败：" + e.getMessage());
        }
        
        return "redirect:/account";
    }

    /**
     * 更新账户设置
     */
    @PostMapping("/update")
    public String updateAccount(@ModelAttribute AccountBalance accountBalance,
                               RedirectAttributes redirectAttributes) {
        try {
            accountService.updateAccountBalance(accountBalance);
            redirectAttributes.addFlashAttribute("success", "账户设置更新成功！");
        } catch (Exception e) {
            redirectAttributes.addFlashAttribute("error", "更新账户设置失败：" + e.getMessage());
        }
        
        return "redirect:/account";
    }
}